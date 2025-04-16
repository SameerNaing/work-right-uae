import { Request } from 'express';

import { IAccessTokenPayload, IRefreshTokenPayload } from './authPayloads';

export interface IRequest extends Request {
  tokenPayload: IAccessTokenPayload;
  refreshTokenPayload: IRefreshTokenPayload;
}
