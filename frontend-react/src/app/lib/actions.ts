'use server'

import {redirect,notFound} from "next/navigation";
import {revalidatePath} from "next/cache";
import {NextResponse} from "next/server";
import {cookies} from "next/headers";

export async function createBucket(prevState: any, formData: FormData) {
    'use server';

    console.log('formData:', formData)
    console.log('prevState:', prevState)

    const rawFormData = {
        title: formData.get('title'),
        description: formData.get('description'),
    };
    // Test it out:
    console.log("rawFormData:", rawFormData);

    const response = await fetch('http://localhost:8000/api/buckets', {
        method: 'POST',
        body: JSON.stringify(rawFormData),
        headers: {
            'Content-Type': 'application/json'
        }
    })

    if (!response.ok) {
        return {
            error:'error creating bucket',
            title: rawFormData.title,
            description: rawFormData.description
        }
    } else {
        revalidatePath('/buckets')
        redirect('/buckets')
    }
}

export async function updateBucket(prevState: any, formData: FormData){

    const bucketId = formData.get('id')
    const response = await fetch(`http://localhost:8000/api/buckets/${bucketId}`, {
        method: 'PATCH',
        headers: {'Content-Type':'application/json'},
        body: JSON.stringify({
            title: formData.get('title'),
            description: formData.get('description')
        })
    })

    if (response.ok) {
        redirect('/buckets')
    } else {
        // TODO reset invalid fields
        return prevState
    }

}

export async function deleteBucket(bucket_id){
    // console.log('in deleteBucket(): bucket_id:', bucket_id)

    const response = await fetch(`http://localhost:8000/api/buckets/${bucket_id}`, {
        method: 'DELETE'
    })

    // await new Promise((resolve) => setTimeout(resolve, 3000))
    if (!response.ok) {
        return {error: `can't delete bucket ${bucket_id}`}
    } else {
        revalidatePath('/buckets')
    }
}

export async function logout() {
    // console.log('in actions logout.ts:')
    const cookieStorage = await cookies()
    cookieStorage.delete('access')
    cookieStorage.delete('refresh')
    revalidatePath('/')
    redirect('/login')
}

export async function getBucket(bucket_id) {
    console.log("in getBucket()")
    const response = await fetch(`http://localhost:8000/api/buckets/${bucket_id}`)

    console.log("response.ok for bucket: ", response.ok, bucket_id)

    if (!response.ok) {
        //return {error: `can't get bucket ${bucket_id}`}
        notFound()
    } else {
        return await response.json()
    }
}

export async function doClientLogin(prevState, formData: FormData){
    // console.log("in doClientLogin")
    const token_response = await fetch(`${process.env.DJANGO_URL}/api/token/`, {
        method: 'POST',
        body: JSON.stringify({username: formData.get('username'), password: formData.get('password')}),
        headers: {'Content-Type':'application/json'}
    })

    if (!token_response.ok) {
        return {error: 'authentication error'}
    }

    const token_data = await token_response.json()
    // console.log("tokens retrieved: ", token_data)

    const cookieStore = cookies()
    cookieStore.set("access", token_data.access, {
        httpOnly: true,
        secure: true,
        sameSite: "strict",
        path: "/",
    })

    cookieStore.set("refresh", token_data.refresh, {
        httpOnly: true,
        secure: true,
        sameSite: "strict",
        path: "/",
    })

    redirect('/buckets')

}
