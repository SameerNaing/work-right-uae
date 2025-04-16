function parseBearerToken(token: string) {
  return token.replace('Bearer ', '').trim();
}

function getUsernameFromEmail(email) {
  let username: string = email.split('@')[0];

  if (username.includes('.')) {
    username = username.split('.').join(' ');
  }

  return username;
}

export const Parsers = { parseBearerToken, getUsernameFromEmail };
