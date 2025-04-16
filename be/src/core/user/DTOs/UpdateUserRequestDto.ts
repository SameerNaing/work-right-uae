import { ApiPropertyOptional } from '@nestjs/swagger';
import { IsOptional, MaxLength } from 'class-validator';

export class UpdateUserRequestDto {
  @ApiPropertyOptional()
  @IsOptional()
  @MaxLength(255)
  name: string;
}
