import {
  CanActivate,
  ExecutionContext,
  Injectable,
  UnauthorizedException,
} from '@nestjs/common';
import { InjectRedis } from '@nestjs-modules/ioredis';
import { Observable } from 'rxjs';
import Redis from 'ioredis';

import { BaseEntity } from 'src/database/base-entity';
import { Parsers } from 'src/functions/parsers';
import { Encryptions } from 'src/functions/encryptions';
import { IRequest, IAccessTokenPayload } from 'src/interfaces';
import { SESSION_REDIS_PREFIX } from 'src/core/user/constants';

@Injectable()
export class OptionalAuthGuard implements CanActivate {
  constructor(@InjectRedis() private readonly redis: Redis) {}

  canActivate(
    context: ExecutionContext,
  ): boolean | Promise<boolean> | Observable<boolean> {
    return new Promise(async (resolve, reject) => {
      const request = context.switchToHttp().getRequest() as IRequest;

      let token = request.headers.authorization;
      if (!token) {
        return resolve(true);
      }

      token = Parsers.parseBearerToken(token);

      try {
        const tokenPayload: IAccessTokenPayload =
          await Encryptions.verifyJwt(token);

        const session = await this.redis.get(
          `${SESSION_REDIS_PREFIX}:${tokenPayload.sessionId}`,
        );

        if (!session) {
          return reject(new UnauthorizedException());
        }

        BaseEntity.setUserId(tokenPayload.id);

        request.tokenPayload = tokenPayload;
        resolve(true);
      } catch (e) {
        return reject(new UnauthorizedException());
      }
    });
  }
}
