import * as jwt from 'jsonwebtoken';
import { v4 as uuidv4 } from 'uuid';

import { environment } from 'src/config/environment';
import { IAccessTokenPayload } from 'src/interfaces';

function signJwt({
  payload,
  secret = environment.authorization.accessTokenSecret,
  signOptions = environment.authorization.signOptions,
}: {
  payload: IAccessTokenPayload;
  secret?: string;
  signOptions?: any;
}) {
  return jwt.sign(payload, secret, signOptions);
}

function verifyJwt(
  token: string,
  jwtSecret = environment.authorization.accessTokenSecret,
  ignoreExpiration: boolean = false,
): IAccessTokenPayload {
  return jwt.verify(token, jwtSecret, {
    ignoreExpiration,
  }) as IAccessTokenPayload;
}

function generateOtp(length = 4) {
  return Math.floor(1000 + Math.random() * 9000).toString();
}

function generateUniqueId() {
  return uuidv4();
}

export const Encryptions = {
  signJwt,
  verifyJwt,
  generateOtp,
  generateUniqueId,
};
