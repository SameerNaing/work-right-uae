import { ApiResponseDto } from 'src/interfaces/DTOs';

export const successHandler = (
  data?: any,
  message: string = '',
): ApiResponseDto => {
  return {
    success: true,
    data: data,
    message,
  };
};
