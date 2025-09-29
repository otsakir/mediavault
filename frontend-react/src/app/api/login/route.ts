import { NextResponse } from "next/server";


export async function POST(request: Request) {

    const {username, password} =  await request.json()

    console.log('DJANGO_URL:', process.env.DJANGO_URL)
    const token_response = await fetch(`${process.env.DJANGO_URL}/api/token/`, {
        method: 'POST',
        body: JSON.stringify({username, password}),
        headers: {'Content-Type':'application/json'}
    })

    const token_data = await token_response.json()

    console.log("tokens retrieved: ", token_data)

    if (token_response.status != 200) {
        console.log('error 1')
        return NextResponse.json({}, {status: token_response.status})
    }

    const response = NextResponse.json({});
    // const  cookies = response.cookies;

    console.log("setting 'access' cookie")
    response.cookies.set("access", token_data.access, {
        httpOnly: true,
        secure: true,
        sameSite: "strict",
        path: "/",
    })

    response.cookies.set("refresh", token_data.refresh, {
        httpOnly: true,
        secure: true,
        sameSite: "strict",
        path: "/",
    })

    return response
}
