import { Body, Controller, Delete, Post, Req, UseGuards } from '@nestjs/common';
import {
  ApiBearerAuth,
  ApiBody,
  ApiHeader,
  ApiOperation,
  ApiResponse,
  ApiTags,
} from '@nestjs/swagger';

import { AuthService } from './auth.service';
import {
  AuthTokenResponseDto,
  LoginRequestDto,
  LoginResponseDto,
  RestoreAccountRequestDto,
  SentOtpRequestDto,
} from '../DTOs';
import { IRequest } from 'src/interfaces';
import { successHandler } from 'src/functions/handlers';
import { plainToInstance } from 'class-transformer';
import { AuthGuard } from 'src/guards/auth.guard';
import { TokenRefreshGuard } from 'src/guards/tokenRefresh.guard';
import { MLCoreAuthGuard } from 'src/guards/mlCore.auth.guard';
import {
  ML_CORE_TOKEN_HEADER_KEY,
  ML_CORE_USER_TOKEN_HEADER_KEY,
  REFRESH_TOKEN_HEADER_KEY,
} from 'src/functions/constants';

@ApiTags('Authentication')
@Controller({ path: 'auth', version: '1' })
export class AuthController {
  constructor(private readonly authService: AuthService) {}

  @Post('login')
  @ApiOperation({ summary: 'Login' })
  @ApiResponse({ status: 200, type: LoginResponseDto })
  @ApiBody({ type: LoginRequestDto })
  async login(@Body() loginRequestDto: LoginRequestDto) {
    const data = await this.authService.login(loginRequestDto);

    const res = plainToInstance(LoginResponseDto, data, {
      excludeExtraneousValues: true,
      enableImplicitConversion: true,
    });

    return successHandler(res, 'Login successful');
  }

  @Post('logout')
  @ApiBearerAuth('JWT-Token')
  @ApiOperation({ summary: 'Logout' })
  @ApiResponse({ status: 200, description: 'Logout successful' })
  @UseGuards(AuthGuard)
  async logout(@Req() req: IRequest) {
    await this.authService.logout(
      req.tokenPayload.id,
      req.tokenPayload.sessionId,
    );

    return successHandler(null, 'Logout successful');
  }

  @Post('refresh-token')
  @ApiOperation({ summary: 'Refresh access Token' })
  @ApiResponse({ status: 200, type: AuthTokenResponseDto })
  @ApiHeader({
    name: REFRESH_TOKEN_HEADER_KEY,
    description: 'Refresh token to generate a new access token',
    required: true,
  })
  @UseGuards(TokenRefreshGuard)
  async refreshToken(@Req() req: IRequest) {
    const data = await this.authService.refreshToken(
      req.refreshTokenPayload.sessionId,
      req.refreshTokenPayload.userId,
    );

    const res = plainToInstance(AuthTokenResponseDto, data, {
      excludeExtraneousValues: true,
      enableImplicitConversion: true,
    });

    return successHandler(res, 'Token refreshed successfully');
  }

  @Post('sent-otp')
  @ApiOperation({ summary: 'Send OTP' })
  @ApiResponse({ status: 200, description: 'OTP sent successfully' })
  @ApiBody({ type: SentOtpRequestDto })
  async sentOtp(@Body() sentOtpRequestDto: SentOtpRequestDto) {
    await this.authService.sendOtp(sentOtpRequestDto);

    return successHandler(null, 'OTP sent successfully');
  }

  @Post('restore-account')
  @ApiOperation({ summary: 'Restore user deleted account' })
  @ApiBody({ type: RestoreAccountRequestDto })
  @ApiResponse({
    status: 200,
    type: AuthTokenResponseDto,
    description: 'Account restored successfully',
  })
  async restoreAccount(@Body() body: RestoreAccountRequestDto) {
    const data = await this.authService.restoreAccount(body);

    const res = plainToInstance(AuthTokenResponseDto, data, {
      excludeExtraneousValues: true,
      enableImplicitConversion: true,
    });

    return successHandler(res, 'Account restored successfully');
  }

  @Delete('delete-account')
  @ApiBearerAuth('JWT-Token')
  @ApiOperation({ summary: 'Delete account' })
  @ApiResponse({ status: 200, description: 'Account deleted successfully' })
  @UseGuards(AuthGuard)
  async deleteAccount(@Req() req: IRequest) {
    await this.authService.deleteAccount(req.tokenPayload.id);
    return successHandler(null, 'Account deleted successfully');
  }

  @Post('verify-token')
  @UseGuards(MLCoreAuthGuard)
  @ApiHeader({
    name: ML_CORE_TOKEN_HEADER_KEY,
    description: 'ML core server token',
    required: true,
  })
  @ApiHeader({
    name: ML_CORE_USER_TOKEN_HEADER_KEY,
    description: 'User token to verify',
    required: true,
  })
  @ApiOperation({ summary: 'Verify User token for ML core server' })
  @ApiResponse({ status: 200, description: 'Token verified successfully' })
  @ApiResponse({
    status: 401,
    description: 'If the User token or ML-core token is not valid',
  })
  async verifyToken(@Req() req: IRequest) {
    await this.authService.verifyToken(
      req.headers[ML_CORE_USER_TOKEN_HEADER_KEY] as string,
    );

    return successHandler(null, 'Token verified successfully');
  }
}
