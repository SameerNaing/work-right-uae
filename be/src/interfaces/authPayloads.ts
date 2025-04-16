export interface IAccessTokenPayload {
  id: string;
  sessionId: string;
}

export interface ISessionPayload {
  accessToken: string;
  refreshToken: string;
}

export interface IRefreshTokenPayload {
  sessionId: string;
  userId: string;
}

export interface IOtpPayload {
  otp: string;
  verified: boolean;
  timestamp: number;
}
