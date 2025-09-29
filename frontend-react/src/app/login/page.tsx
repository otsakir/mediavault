import {LoginForm} from "@/app/ui/components";
import {doClientLogin} from "@/app/lib/actions";

export default async function MyLogin() {


    return (<div className="flex flex-col min-h-screen">
        <div className={"w-[400px] m-auto bg-teal-100 rounded-md p-4 text-slate-600 flex flex-col"}>
            <div className={'mb-6'}>
                <h1 className="text-3xl mb-2">Login</h1>
                <h2 className='text-xl font-bold'>M E D I A &nbsp;  V A U L T</h2>
            </div>
            <LoginForm serverFunction={doClientLogin}/>

        </div>
    </div>)
}