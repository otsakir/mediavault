'use client'

import { useActionState} from "react";
import {createBucket} from "@/app/lib/actions";
import {BucketForm} from "@/app/ui/components";

export default function NewBucket() {

    // const [state, formAction, pending] = useActionState(createBucket, {
    // })

    const initialState = {
        message: '',
        title: '',
        description: ''
    }


    return (
        <div className="text-slate-700">
            <div className="flex items-center justify-between mb-4 border-b py-2 border-slate-200">
                <h1 className="text-3xl">New bucket</h1>
            </div>
            <BucketForm serverFunction={createBucket} initialState={initialState} />
        </div>
    )

}