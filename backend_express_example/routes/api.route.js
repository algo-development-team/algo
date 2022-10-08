const router = require('express').Router()
const { google } = require('googleapis')

const GOOGLE_CLIENT_ID = 'YOUR_GOOGLE_CLIENT_ID'
const GOOGLE_CLIENT_SECRET = 'YOUR_GOOGLE_CLIENT_SECRET'

const REFRESH_TOKEN = 'YOUR_REFRESH_TOKEN'

const oauth2Client = new google.auth.OAuth2(
  GOOGLE_CLIENT_ID,
  GOOGLE_CLIENT_SECRET,
  'http://localhost:3000',
)

router.get('/', async (req, res, next) => {
  res.send({ message: 'Ok api is working 🚀' })
})

router.post('/create-tokens', async (req, res, next) => {
  try {
    const { code } = req.body
    const { tokens } = await oauth2Client.getToken(code)
    res.send(tokens)
  } catch (error) {
    next(error)
  }
})

router.post('/create-event', (req, res, next) => {
  try {
    const { summary, description, location, startDateTime, endDateTime } =
      req.body

    const event = {
      summary: summary,
      description: description,
      location: location,
      colorId: '7',
      start: {
        dateTime: new Date(startDateTime),
      },
      end: {
        dateTime: new Date(endDateTime),
      },
    }

    oauth2Client.setCredentials({ refresh_token: REFRESH_TOKEN })
    const calendar = google.calendar('v3')
    calendar.events.insert(
      {
        auth: oauth2Client,
        calendarId: 'primary',
        resource: event,
        // requestBody: {
        //   summary: summary,
        //   description: description,
        //   location: location,
        //   colorId: '7',
        //   start: {
        //     dateTime: new Date(startDateTime),
        //   },
        //   end: {
        //     dateTime: new Date(endDateTime),
        //   },
        // },
      },
      (err, event) => {
        if (err) {
          console.log(
            'There was an error contacting the Calendar service: ' + err,
          )
          return
        }
        console.log('Event created: %s', event.htmlLink)
      },
    )
    res.send({ msg: 'event added' })
  } catch (error) {
    next(error)
  }
})

module.exports = router

/*
Color ID:
1 blue
2 green
3 purple
4 red
5 yellow
6 orange
7 turquoise
8 grey
9 bold blue
10 bold green
11 bold red
*/
