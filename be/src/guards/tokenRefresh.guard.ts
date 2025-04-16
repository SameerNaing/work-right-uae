import {
  CanActivate,
  ExecutionContext,
  Injectable,
  UnauthorizedException,
} from '@nestjs/common';
import { Redis } from 'ioredis';
import { Observable } from 'rxjs';
import { InjectRedis } from '@nestjs-modules/ioredis';

import { environment } from 'src/config/environment';
import { IRequest } from 'src/interfaces/global';
import { IRefreshTokenPayload } from 'src/interfaces';
import { REFRESH_REDIS_PREFIX } from 'src/core/user/constants';
import { REFRESH_TOKEN_HEADER_KEY } from 'src/functions/constants';

@Injectable()
export class TokenRefreshGuard implements CanActivate {
  constructor(@InjectRedis() private readonly redis: Redis) {}

  canActivate(
    context: ExecutionContext,
  ): boolean | Promise<boolean> | Observable<boolean> {
    return new Promise(async (resolve, reject) => {
      try {
        const request = context.switchToHttp().getRequest() as IRequest;

        let token = request.headers[REFRESH_TOKEN_HEADER_KEY];

        if (!token) {
          reject(new UnauthorizedException('Token not found in request'));
          return;
        }

        const storedToken = await this.redis.get(
          `${REFRESH_REDIS_PREFIX}:${token}`,
        );

        if (!storedToken) {
          reject(new UnauthorizedException('Token Expired'));
          return;
        }

        const tokenPayload = JSON.parse(storedToken) as IRefreshTokenPayload;

        request.refreshTokenPayload = tokenPayload;

        resolve(true);
      } catch (e) {
        reject(new UnauthorizedException('Invalid token'));
      }
    });
  }
}
