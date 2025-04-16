import {
  CanActivate,
  ExecutionContext,
  Injectable,
  UnauthorizedException,
} from '@nestjs/common';
import { Observable } from 'rxjs';

import { BaseEntity } from 'src/database/base-entity';
import { IRequest } from 'src/interfaces';
import { Parsers } from 'src/functions/parsers';
import { Encryptions } from 'src/functions/encryptions';
import { ML_CORE_TOKEN_HEADER_KEY } from 'src/functions/constants';

@Injectable()
export class MLCoreAuthGuard implements CanActivate {
  constructor() {}

  canActivate(
    context: ExecutionContext,
  ): boolean | Promise<boolean> | Observable<boolean> {
    return new Promise(async (resolve, reject) => {
      try {
        const request = context.switchToHttp().getRequest() as IRequest;

        let token = request.headers[ML_CORE_TOKEN_HEADER_KEY] as string;

        if (!token) {
          reject(new UnauthorizedException());
          return;
        }

        token = Parsers.parseBearerToken(token);

        Encryptions.verifyJwt(token);

        resolve(true);

        resolve(true);
      } catch (e) {
        reject(new UnauthorizedException());
      }
    });
  }
}
