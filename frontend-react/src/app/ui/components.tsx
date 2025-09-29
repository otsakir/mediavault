'use client'

import {usePathname} from "next/navigation";
import Link from "next/link";
import {Trash} from "lucide-react";
import {deleteBucket, logout} from "@/app/lib/actions";
import {useState} from "react";
import {useActionState} from "react";


export function MainMenu({menuitems}) {
    const pathname = usePathname()

    function onLogoutClick() {
        console.log("Logout clicked")
        logout()
    }

    return <div className = "flex gap-4">
            {
                menuitems.map((item) => {
                    return pathname === item.href ? <span key={item.href} className='underline'>{item.label}</span> :
                        <Link key={item.href} className='hover:underline' href={item.href}>{item.label}</Link>
                })
            }
            <button onClick={onLogoutClick} className='hover:underline'>Logout</button>

    </div>
}


export function TrashButton({bucket}) {

    const [pending, setPending] = useState(false);

    async function trashClicked() {
        setPending(true)
        const response =  await deleteBucket(bucket.id)
        if (response?.error) {
            setPending(false)
        }
    }

    return <button disabled={pending} onClick={trashClicked}>
            <div className='bg-teal-200 rounded-md p-2 mb-2 hover:bg-teal-400'>
                <Trash className="h-4 w-4 text-gray-600 transition-colors"/>
            </div>
    </button>

}

export function BucketForm({serverFunction, initialState, bucketId}) {

    const [formState, formAction, isPending] = useActionState(serverFunction, initialState)

    return <form action={formAction}>
        <div className="mb-4">
            <label className="block">Title</label>
            <input defaultValue={formState.title} type='text' name='title'
                   className="shadow appearance-none border rounded w-full py-2 px-3 mb-3 leading-tight focus:outline-none focus:shadow-outline"/>
        </div>
        <div className="mb-4">
            <label className="block">Description</label>
            <textarea defaultValue={formState.description} name='description'
                      className="h-40 shadow appearance-none border rounded w-full py-2 px-3 mb-3 leading-tight focus:outline-none focus:shadow-outline"/>
        </div>
        {bucketId ? <input type='hidden' name='id' value={bucketId} /> : ''}
        <input className="hover:bg-red-500 text-white px-4 p-2 bg-black rounded-md" type="submit" value={bucketId ? 'Update' : 'Create'}/>
    </form>
}


export function LoginForm({serverFunction}) {

    const initialState = {
        username : '',
        password : ''
    }
    const [formState, formAction, isPending] = useActionState(serverFunction, initialState)

    return <form action={formAction}>
        <div className={'mb-4'}>
            <label className='block mb-2' htmlFor='username'>Username</label>
            <input defaultValue={formState.username} id='usernane' name='username' className='p-2 rounded-md w-full bg-white focus:outline-none'/>
        </div>
        <div className={'mb-2'}>
            <label className='block mb-2' htmlFor='password'>Password</label>
            <input defaultValue={formState.password} id='password' name='password' type={'password'}
                   className='p-2 rounded-md w-full bg-white focus:outline-none'/>
        </div>
        <div className='text-red-400'>
            {formState?.error ? formState.error : ''}
        </div>

        <button className='mt-4 p-2 px-4 rounded-md bg-teal-700 text-white hover:bg-teal-600' type='submit'>Login</button>

    </form>
}