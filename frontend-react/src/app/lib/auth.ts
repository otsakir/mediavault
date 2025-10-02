import {UserInfo} from '@/app/lib/types'
import {cookies} from "next/headers";

const decodeJwt = (token: string): any => {
  try {
    // Split the token into parts
    const parts = token.split('.');
    if (parts.length !== 3) {
      throw new Error('Invalid JWT token');
    }

    // Base64 decode the payload
    const payload = parts[1];
    const decoded = atob(payload.replace(/-/g, '+').replace(/_/g, '/'));

    return JSON.parse(decoded);
  } catch (error) {
    console.error('JWT decoding failed:', error);
    return null;
  }
};


export async function getUserInfo() {

    const cookieStorage = await cookies()

    const accessToken = cookieStorage.get('access')?.value
    if (!accessToken)
        return {}

    const tokenJson = decodeJwt(accessToken)

    const userinfo = {
        id: tokenJson.user_id,
        username: tokenJson.username,
        email: tokenJson.email,
        permission_ids: tokenJson?.permission_ids
    }

    console.log('auth.ts: access cookie: ', accessToken, tokenJson)
    console.log('auth.ts: userinfo:', userinfo)

    return userinfo
}