import { ApiProperty } from '@nestjs/swagger';
import { IsEmail, IsNotEmpty } from 'class-validator';

export class SentOtpRequestDto {
  @ApiProperty()
  @IsEmail()
  @IsNotEmpty()
  email: string;
}
