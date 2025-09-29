import { NextResponse } from "next/server";
import type { NextRequest } from "next/server";


export async function middleware(req: NextRequest) {
  const access = req.cookies.get("access")?.value
  const refresh = req.cookies.get("refresh")?.value

  if (req.nextUrl.pathname.startsWith("/buckets") && !access && !refresh) {
    return NextResponse.redirect(new URL("/login", req.url))
  }

  // try to refresh if there is no access token
  if (!access) {
    console.log("middleware.ts: refreshing access token...")
    const res = await fetch(`${process.env.DJANGO_URL}/api/token/refresh/`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ refresh }),
    })

    if (!res.ok) {
      console.log('middleware.ts: refresh failed, redirecting to /login. status: ', res.status)
      // TODO handle other types of server errors besides auth errors here
      return NextResponse.redirect(new URL("/login", req.url))
    }
    // console.log('middleware.ts: refresh returned status code: ', res.status)
    const { access } = await res.json()
    // console.log('middleware.ts: new access token:', access )

    // set new access token cookie
    // console.log('middleware.ts: setting new access cookie')
    const response = NextResponse.next()
    response.cookies.set('access', access, {
      httpOnly: true,
      secure: true,
      path: '/',
      maxAge: 60,
      sameSite: 'strict',
    })

    return response
  }

  return NextResponse.next()
}


export const config = {
  matcher: ["/buckets/:path*","/community/:path*"], // paths that need auth
};