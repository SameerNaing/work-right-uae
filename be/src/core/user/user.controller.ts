import {
  Body,
  Controller,
  Delete,
  Get,
  Patch,
  Post,
  Req,
  UseGuards,
} from '@nestjs/common';
import {
  ApiBearerAuth,
  ApiBody,
  ApiHeader,
  ApiOperation,
  ApiResponse,
  ApiTags,
} from '@nestjs/swagger';
import { InjectRepository } from '@nestjs/typeorm';

import { UserEntity } from 'src/database/auth/user.entity';
import { IRequest } from 'src/interfaces';
import { UserService } from './user.service';
import { plainToInstance } from 'class-transformer';
import { UpdateUserRequestDto, UserMeResponseDto } from './DTOs';
import { successHandler } from 'src/functions/handlers';
import { AuthGuard } from 'src/guards/auth.guard';

@ApiTags('Users')
@ApiBearerAuth('JWT-Token')
@Controller({ path: 'users', version: '1' })
export class UserController {
  constructor(private readonly userService: UserService) {}

  @Get('me')
  @UseGuards(AuthGuard)
  @ApiOperation({ summary: 'Get the current login user info' })
  @ApiResponse({
    status: 200,
    description: 'User information retrieved successfully',
  })
  async getMeUser(@Req() req: IRequest) {
    const user = await this.userService.findById(req.tokenPayload.id, {
      select: { id: true, email: true, name: true },
    });

    const res = plainToInstance(UserMeResponseDto, user, {
      excludeExtraneousValues: true,
      enableImplicitConversion: true,
    });

    return successHandler(res, 'User information retrieved successfully');
  }

  @Patch('me')
  @UseGuards(AuthGuard)
  @ApiOperation({ summary: 'Update the current login user info' })
  @ApiResponse({
    status: 200,
    description: 'User information updated successfully',
  })
  @ApiBody({ type: UpdateUserRequestDto })
  async updateMeUser(
    @Req() req: IRequest,
    @Body() userData: UpdateUserRequestDto,
  ) {
    await this.userService.updateUser(req.tokenPayload.id, userData);
    return successHandler(null, 'User information updated successfully');
  }
}
