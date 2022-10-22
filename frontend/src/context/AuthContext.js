import React, { createContext, useContext, useState, useEffect } from 'react'
import { auth, createUserProfileDocument, provider } from '_firebase'
import {
  signInWithPopup,
  signInWithEmailAndPassword,
  createUserWithEmailAndPassword,
  signOut,
  signInWithRedirect,
} from 'firebase/auth'
import { onSnapshot, updateDoc } from 'firebase/firestore'
import { getAuth, updateProfile } from 'firebase/auth'
import { Navigate, useNavigate } from 'react-router-dom'

export const AuthContext = createContext()
export const AuthProvider = ({ children }) => {
  const [currentUser, setCurrentUser] = useState({})
  const [loading, setLoading] = useState(true)
  let navigate = useNavigate()
  const authUser = getAuth()

  const setDisplayName = (name) => {
    updateProfile(authUser.currentUser, {
      displayName: name,
    }).catch((error) => {
      // An error occurred
      // ...
    })
  }
  const signinWithEmail = (email, password) => {
    return signInWithEmailAndPassword(auth, email, password).then((cred) => {
      setCurrentUser(cred.user)
      localStorage.setItem('userAuth', JSON.stringify(cred.user))
      navigate('/app/Inbox')
    })
  }

  const signupWithEmail = async ({ email, password, name }) => {
    //Todo: reutrn the function below and perform routing in signup component
    return createUserWithEmailAndPassword(auth, email, password).then(
      (cred) => {
        setDisplayName(name)
        setCurrentUser({ ...cred.user, displayName: name })
        localStorage.setItem('userAuth', JSON.stringify(cred.user))
        navigate('/app/Inbox')
      },
    )
  }

  const signinGoogle = (e) => {
    e.preventDefault()
    signInWithPopup(auth, provider)
      .then((result) => {
        const user = result.user
        setCurrentUser(user)
        localStorage.setItem('userAuth', JSON.stringify(user))
        // DEBUG
        console.log('signinGoogle ran...')
        console.log(JSON.stringify(user))
        navigate('/app/Inbox')
      })
      .catch((error) => {
        const errorCode = error.code
        const errorMessage = error.message
        console.log(errorCode, ':', errorMessage)
      })
  }

  const signout = () => {
    const userAuth = getAuth()

    signOut(userAuth)
      .then(() => {
        setCurrentUser(null)
        localStorage.removeItem('userAuth')
      })
      .finally(() => navigate('/'))
  }

  useEffect(() => {
    const getMissingFieldValuePairsInUser = (snapshotData) => {
      const defaultRankings = new Array(24).fill(50)
      const fieldValuePairs = [
        ['refreshToken', null],
        ['workTimeRange', '9:00-17:00'],
        ['sleepTimeRange', '23:00-07:00'],
        ['workDays', [false, true, true, true, true, true, false]],
        ['isSetup', false],
        ['calendarId', null],
        ['checklist', []],
        ['urgentRankingsWw', defaultRankings],
        ['deepRankingsWw', defaultRankings],
        ['shallowRankingsWw', defaultRankings],
        ['urgentRankingsPw', defaultRankings],
        ['deepRankingsPw', defaultRankings],
        ['shallowRankingsPw', defaultRankings],
        ['urgentRankingsPnw', defaultRankings],
        ['deepRankingsPnw', defaultRankings],
        ['shallowRankingsPnw', defaultRankings],
      ]
      let missingFieldValuePairs = fieldValuePairs.filter(
        (fieldValuePair) => !snapshotData[fieldValuePair[0]],
      )
      missingFieldValuePairs = Object.fromEntries(missingFieldValuePairs)
      return missingFieldValuePairs
    }
    const unsubscribe = auth.onAuthStateChanged(async (userAuth) => {
      setLoading(false)
      if (userAuth) {
        const userRef = await createUserProfileDocument(userAuth)
        // DEBUG
        console.log('unsubscribe ran...')
        console.log('userAuth: ', userAuth)
        console.log('userRef: ', userRef)
        onSnapshot(userRef, (snapshot) => {
          const snapshotData = snapshot.data()
          const missingFieldValuePairs =
            getMissingFieldValuePairsInUser(snapshotData)
          if (Object.keys(missingFieldValuePairs).length > 0) {
            updateDoc(userRef, missingFieldValuePairs)
          }
          const user = {
            displayName: snapshotData.displayName,
            email: snapshotData.email,
            id: snapshot.id,
          }
          // DEBUG
          console.log('user: ', user)
          setCurrentUser(user)

          localStorage.setItem('userAuth', JSON.stringify(user))
        })
      } else {
        setCurrentUser(userAuth)
      }
    })

    return () => unsubscribe()
  }, [])

  // useEffect(() => {
  //   return !currentUser ? navigate("/") : null;
  // }, [currentUser]);
  const authValue = {
    currentUser,
    signupWithEmail,
    signinWithEmail,
    signinGoogle,
    signout,
  }

  return (
    <AuthContext.Provider value={authValue}>
      {!loading && children}
    </AuthContext.Provider>
  )
}
export default AuthProvider
