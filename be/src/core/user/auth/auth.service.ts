import {
  BadRequestException,
  Injectable,
  Logger,
  UnauthorizedException,
} from '@nestjs/common';
import { InjectRedis } from '@nestjs-modules/ioredis';
import { Redis } from 'ioredis';

import {
  LoginRequestDto,
  RestoreAccountRequestDto,
  SentOtpRequestDto,
} from '../DTOs';
import { Encryptions } from 'src/functions/encryptions';
import { UserService } from '../user.service';
import {
  IAccessTokenPayload,
  IOtpPayload,
  IRefreshTokenPayload,
} from 'src/interfaces';
import {
  OTP_REDIS_PREFIX,
  REFRESH_REDIS_PREFIX,
  SESSION_REDIS_PREFIX,
  USER_SESSIONS_REDIS_PREFIX,
} from '../constants';
import { environment } from 'src/config/environment';
import { Parsers } from 'src/functions/parsers';

@Injectable()
export class AuthService {
  private readonly logger = new Logger(AuthService.name);

  constructor(
    @InjectRedis() private readonly redis: Redis,
    private readonly userService: UserService,
  ) {}

  async login(body: LoginRequestDto) {
    const key = `${OTP_REDIS_PREFIX}:${body.email}`;

    const redisData = await this.redis.get(key);

    if (!redisData) {
      this.logger.error({
        message: 'OTP not found',
        email: body.email,
      });
      throw new BadRequestException('OTP Expired');
    }
    const parsedRedisData = JSON.parse(redisData) as IOtpPayload;

    if (parsedRedisData.otp !== body.otp) {
      this.logger.error({
        message: 'Invalid OTP',
        email: body.email,
      });
      throw new BadRequestException('Invalid OTP');
    }

    let user = await this.userService.findByEmail(body.email, {
      select: { id: true, deletedAt: true },
      withDeleted: true,
      throwError: false,
    });

    if (user?.deletedAt) {
      this.logger.log({
        message: 'User account deleted',
        email: body.email,
        deletedAt: user.deletedAt,
      });

      // extends for 1 min
      await this.redis.set(
        key,
        JSON.stringify({ ...parsedRedisData, verified: true }),
        'EX',
        60 * 2,
      );

      return { isAccountDeleted: true };
    }

    if (!user) {
      const username = Parsers.getUsernameFromEmail(body.email);
      user = await this.userService.createUser({
        name: username,
        email: body.email,
      });
    }

    await this.redis.del(key);

    return await this.authorizeUser(user!.id);
  }

  async sendOtp(body: SentOtpRequestDto) {
    const key = `${OTP_REDIS_PREFIX}:${body.email}`;
    const otpPayload: IOtpPayload = {
      otp: Encryptions.generateOtp(),
      verified: false,
      timestamp: Date.now(),
    };
    const oneMinute = 60 * 1000;
    const threeMinutes = 60 * 3;

    const redisData = await this.redis.get(key);

    if (redisData) {
      const parsedData = JSON.parse(redisData);
      const currentTime = Date.now();
      if (parsedData.timestamp + oneMinute > currentTime)
        this.logger.error({
          message:
            'OTP was sent recently, please wait for one minute before sending again',
          currentTime,
          lastSentTime: parsedData.timestamp,
          timeDifference: currentTime - parsedData.timestamp,
        });
      throw new BadRequestException(
        'OTP was sent recently, please wait for one minute before sending again',
      );
    }

    await this.redis.set(key, JSON.stringify(otpPayload), 'EX', threeMinutes);

    this.logger.log({
      message: 'OTP sent successfully',
      email: body.email,
      otp: otpPayload.otp,
      timestamp: otpPayload.timestamp,
    });

    return;
  }

  async restoreAccount(body: RestoreAccountRequestDto) {
    const key = `${OTP_REDIS_PREFIX}:${body.email}`;

    const redisData = await this.redis.get(key);

    if (!redisData) {
      this.logger.error({
        message: 'Session Expired',
        email: body.email,
      });
      throw new BadRequestException('Session Expired');
    }
    const parsedRedisData = JSON.parse(redisData) as IOtpPayload;

    if (!parsedRedisData.verified) {
      this.logger.error({
        message: 'OTP not verified',
        email: body.email,
        redisData: parsedRedisData,
      });
      throw new BadRequestException('Please verify your email first');
    }

    const user = await this.userService.findByEmail(body.email, {
      select: { id: true },
      withDeleted: true,
    });

    await this.userService.restoreUser(user!.id);

    await this.redis.del(key);

    return await this.authorizeUser(user!.id);
  }

  async logout(userId: string, sessionId: string) {
    await this.removeUserSession(userId, sessionId);

    this.logger.log({
      message: 'User logged out successfully',
      userId,
      sessionId,
    });

    return;
  }

  async deleteAccount(userId: string) {
    await Promise.all([
      this.removeAllUserSessions(userId),
      this.userService.deleteUser(userId),
    ]);

    return;
  }

  async refreshToken(sessionId: string, userId: string) {
    const [_, tokens] = await Promise.all([
      this.removeUserSession(userId, sessionId),
      this.authorizeUser(userId),
    ]);

    return tokens;
  }

  async verifyToken(userToken: string) {
    const token = Encryptions.verifyJwt(
      userToken,
      environment.authorization.accessTokenSecret,
      true,
    );

    const session = await this.redis.get(
      `${SESSION_REDIS_PREFIX}:${token.sessionId}`,
    );

    if (!session) {
      this.logger.error({
        message: 'Session not found',
        sessionId: token.sessionId,
      });
      throw new UnauthorizedException('Session not found');
    }

    return;
  }

  private async authorizeUser(userId: string) {
    const { sessionId, refreshToken } = await this.saveUserSession(userId);

    const accessToken = this.generateAccessToken(userId, sessionId);

    return {
      accessToken,
      refreshToken,
    };
  }

  private generateAccessToken(userId: string, sessionId: string) {
    const payload: IAccessTokenPayload = {
      id: userId,
      sessionId,
    };

    return Encryptions.signJwt({ payload });
  }

  private async removeAllUserSessions(userId: string) {
    const sessions = await this.redis.lrange(
      `${USER_SESSIONS_REDIS_PREFIX}:${userId}`,
      0,
      -1,
    );

    if (!sessions) {
      this.logger.debug({
        message: 'No sessions found for user',
        userId,
      });
      return;
    }

    await Promise.all(
      sessions.map((sessionId) => this.removeUserSession(userId, sessionId)),
    );

    return;
  }

  private async removeUserSession(userId: string, sessionId: string) {
    const session = await this.redis.get(
      `${SESSION_REDIS_PREFIX}:${sessionId}`,
    );

    if (!session) {
      this.logger.debug({
        message: 'Session not found',
        sessionId,
        userId,
      });
      return;
    }

    const refreshToken = JSON.parse(session).refreshToken;

    await this.redis.del(`${SESSION_REDIS_PREFIX}:${sessionId}`);
    await this.redis.lrem(
      `${USER_SESSIONS_REDIS_PREFIX}:${userId}`,
      0,
      sessionId,
    );
    await this.redis.del(`${REFRESH_REDIS_PREFIX}:${refreshToken}`);
  }

  private async saveUserSession(userId: string) {
    const refreshToken = Encryptions.generateUniqueId();
    const sessionId = Encryptions.generateUniqueId();

    await this.redis.rpush(
      `${USER_SESSIONS_REDIS_PREFIX}:${userId}`,
      sessionId,
    );

    await this.redis.set(
      `${SESSION_REDIS_PREFIX}:${sessionId}`,
      JSON.stringify({ userId, refreshToken }),
      'EX',
      environment.authorization.sessionExpiryTime,
    );

    await this.redis.set(
      `${REFRESH_REDIS_PREFIX}:${refreshToken}`,
      JSON.stringify({ userId, sessionId }),
      'EX',
      environment.authorization.sessionExpiryTime,
    );

    return { refreshToken, sessionId };
  }
}
