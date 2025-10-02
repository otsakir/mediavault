'use client'

import {createContext, useContext, useEffect} from "react";

const AuthContext = createContext({})



export function AuthProvider({children}) {


    // state
    // ...

    async function processAuthCookies() {
        //const accessCookie = getCookie('access')
        //console.log('processAuthCookies: access cookie:', accessCookie)
    }

    useEffect(() => {
        processAuthCookies()
    },[])



    return (<>
        <AuthContext.Provider value={processAuthCookies}>
            {children}
        </AuthContext.Provider>
    </>)

}

export const useAuth = () => useContext(AuthContext)
