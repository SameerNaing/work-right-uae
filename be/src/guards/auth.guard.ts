import {
  CanActivate,
  ExecutionContext,
  Injectable,
  UnauthorizedException,
} from '@nestjs/common';
import Redis from 'ioredis';
import { Observable } from 'rxjs';
import { InjectRedis } from '@nestjs-modules/ioredis';

import { BaseEntity } from 'src/database/base-entity';
import { IRequest } from 'src/interfaces';
import { Parsers } from 'src/functions/parsers';
import { Encryptions } from 'src/functions/encryptions';
import { IAccessTokenPayload } from '../interfaces';
import { SESSION_REDIS_PREFIX } from 'src/core/user/constants';

@Injectable()
export class AuthGuard implements CanActivate {
  constructor(@InjectRedis() private readonly redis: Redis) {}

  canActivate(
    context: ExecutionContext,
  ): boolean | Promise<boolean> | Observable<boolean> {
    return new Promise(async (resolve, reject) => {
      const request = context.switchToHttp().getRequest() as IRequest;

      let token = request.headers.authorization;
      if (!token) {
        reject(new UnauthorizedException());
        return;
      }

      token = Parsers.parseBearerToken(token);

      try {
        const tokenPayload: IAccessTokenPayload = Encryptions.verifyJwt(token);

        const session = await this.redis.get(
          `${SESSION_REDIS_PREFIX}:${tokenPayload.sessionId}`,
        );

        if (!session) {
          reject(new UnauthorizedException());
          return;
        }

        BaseEntity.setUserId(tokenPayload.id);

        request.tokenPayload = tokenPayload;

        resolve(true);
      } catch (e) {
        reject(new UnauthorizedException());
      }
    });
  }
}
