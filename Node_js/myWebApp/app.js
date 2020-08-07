// Express JS App
// If you make changes to the below code, ensure that you Ctrl C out of the last run in the terminal
// and then re-launch the updated script.

const express = require('express')
const app = express()
const port = 3000

app.get('/', (req, res) => res.send('Hello World .. Compliments from Express JS and Node JS .. Quite a feat, isnt?'))

app.listen(port, () => console.log(`Example app listening at http://localhost:${port}`))