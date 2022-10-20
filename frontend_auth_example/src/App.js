import { useEffect, useState } from 'react'
import './App.css'
import { GoogleLogin, GoogleLogout } from 'react-google-login'
import { gapi } from 'gapi-script'
import axios from 'axios'

function App() {
  const [summary, setSummary] = useState('')
  const [description, setDescription] = useState('')
  const [location, setLocation] = useState('')
  const [startDateTime, setStartDateTime] = useState('')
  const [endDateTime, setEndDateTime] = useState('')
  const [signedIn, setSignedIn] = useState(false)

  useEffect(() => {
    gapi.load('client:auth2', () => {
      gapi.auth2.init({
        clientId: process.env.REACT_APP_CLIENT_ID,
        scope: 'openid email profile https://www.googleapis.com/auth/calendar',
      })
    })
  }, [])

  const responseGoogle = (response) => {
    console.log(response)
    const { code } = response
    axios
      .put(`${process.env.REACT_APP_SERVER_URL}/api/auth/create-tokens`, {
        code,
      })
      .then((response) => {
        console.log(response.data)
        setSignedIn(true)
      })
      .catch((error) => {
        console.log(error.message)
      })
  }

  const responseError = (error) => {
    console.log(error)
  }

  const responseLogout = (response) => {
    console.log(response)
  }

  const handleSubmit = (e) => {
    e.preventDefault()
    // console.log(summary, description, location, startDateTime, endDateTime)
    axios
      .post(`${process.env.REACT_APP_SERVER_URL}/api/auth/create-event`, {
        summary,
        description,
        location,
        startDateTime,
        endDateTime,
      })
      .then((response) => {
        console.log(response.data)
      })
      .catch((error) => console.log(error.message))
  }

  return (
    <div>
      <div className='App'>
        <h1>Google Calendar API</h1>
      </div>
      {!signedIn ? (
        <div>
          <GoogleLogin
            clientId={process.env.REACT_APP_CLIENT_ID}
            buttonText='Sign in & Authorize Calendar'
            onSuccess={responseGoogle}
            onFailure={responseError}
            cookiePolicy={'single_host_origin'}
            // This is important
            responseType='code'
            // prompt='consent'
            accessType='offline'
            scope='openid email profile https://www.googleapis.com/auth/calendar'
          />
        </div>
      ) : (
        <div>
          {/* <GoogleLogout
            clientId={clientId}
            buttonText='Logout'
            onLogoutSuccess={responseLogout}
          /> */}
          <form onSubmit={handleSubmit}>
            <label htmlFor='summary'>Summary</label>
            <br />
            <input
              type='text'
              id='summary'
              value={summary}
              onChange={(e) => setSummary(e.target.value)}
            />
            <br />

            <label htmlFor='description'>Description</label>
            <br />
            <textarea
              type='text'
              id='description'
              value={description}
              onChange={(e) => setDescription(e.target.value)}
            />
            <br />

            <label htmlFor='location'>Location</label>
            <br />
            <input
              type='text'
              id='location'
              value={location}
              onChange={(e) => setLocation(e.target.value)}
            />
            <br />

            <label htmlFor='startDateTime'>Start Date Time</label>
            <br />
            <input
              type='datetime-local'
              id='startDateTime'
              value={startDateTime}
              onChange={(e) => setStartDateTime(e.target.value)}
            />
            <br />

            <label htmlFor='endDateTime'>End Date Time</label>
            <br />
            <input
              type='datetime-local'
              id='endDateTime'
              value={endDateTime}
              onChange={(e) => setEndDateTime(e.target.value)}
            />
            <br />
            <button type='submit'>create event</button>
          </form>
        </div>
      )}
    </div>
  )
}

export default App
