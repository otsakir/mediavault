import Image from "next/image";
import {MainMenu} from "@/app/ui/components";

const menuitems = [
    {href: '/buckets', label: 'Buckets'},
    {href: '/community', label: 'Community'},
    {href: '/logout', label: 'Logout'},
]


export default function Main({children}) {


    return (<div>

        <div className="flex items-center justify-between p-8">
            <a href='/'>
                <div className="flex items-center gap-4">
                    <Image src="/logo.svg" className="w-10" alt="logo" width={100} height={100}/>
                    <h1 className="text-3xl font-bold text-slate-700">Media Vault</h1>
                </div>
            </a>

            <MainMenu menuitems={menuitems} />


        </div>
        <div className="flex flex-col">
            <div className="container mx-auto max-w-screen-lg mb-8">
                {children}
            </div>
        </div>



    </div>)
}