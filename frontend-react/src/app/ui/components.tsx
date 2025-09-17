'use client'

import {usePathname} from "next/navigation";
import Link from "next/link";


export function MainMenu({menuitems}) {
    const pathname = usePathname()

        return <div className = "flex gap-4">
                {
                    menuitems.map((item) => {
                        return pathname === item.href ? <span key={item.href} className='underline'>{item.label}</span> :
                            <Link key={item.href} className='hover:underline' href={item.href}>{item.label}</Link>
                    })
                }
        </div>
}