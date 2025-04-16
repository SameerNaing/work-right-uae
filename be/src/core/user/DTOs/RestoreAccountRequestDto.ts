import { ApiProperty } from '@nestjs/swagger';
import { IsEmail, IsNotEmpty } from 'class-validator';

export class RestoreAccountRequestDto {
  @ApiProperty()
  @IsEmail()
  @IsNotEmpty()
  email: string;
}
