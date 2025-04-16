import { ApiResponseProperty } from '@nestjs/swagger';
import { Expose } from 'class-transformer';

@Expose()
export class AuthTokenResponseDto {
  @ApiResponseProperty()
  @Expose()
  accessToken: string;

  @ApiResponseProperty()
  @Expose()
  refreshToken: string;
}

@Expose()
export class LoginResponseDto extends AuthTokenResponseDto {
  @ApiResponseProperty()
  @Expose()
  isAccountDeleted: boolean;
}
