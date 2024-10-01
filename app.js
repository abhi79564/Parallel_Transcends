const express = require('express')
const path = require('path')
const app = express()
const PORT = process.env.PORT || 4000

const server = app.listen(PORT, () => console.log(`💬 server on port ${PORT}`))

const io = require('socket.io')(server, {
  maxHttpBufferSize: 1e7 // 10 MB max file size
})

app.use(express.static(path.join(__dirname, 'public')))

let socketsConected = new Set()

io.on('connection', onConnected)

function onConnected(socket) {
  console.log('Socket connected', socket.id)
  socketsConected.add(socket.id)
  
  // Emit the total number of connected clients
  io.emit('clients-total', socketsConected.size)

  socket.on('disconnect', () => {
    console.log('Socket disconnected', socket.id)
    socketsConected.delete(socket.id)
    // Emit the updated total number of connected clients
    io.emit('clients-total', socketsConected.size)
  })

  // Handle incoming messages
  socket.on('message', (data) => {
    console.log('Message received:', data.name, data.message)
    // Broadcast the message to all other connected clients
    socket.broadcast.emit('chat-message', data)
  })

  // Handle typing feedback
  socket.on('feedback', (data) => {
    socket.broadcast.emit('feedback', data)
  })
}

// Serve index.html for the root route
app.get('/', (req, res) => {
  res.sendFile(path.join(__dirname, 'public', 'index.html'))
})

// Error handling middleware
app.use((err, req, res, next) => {
  console.error(err.stack)
  res.status(500).send('Something broke!')
})

// 404 handler
app.use((req, res, next) => {
  res.status(404).send("Sorry, can't find that!")
})

process.on('unhandledRejection', (reason, promise) => {
  console.log('Unhandled Rejection at:', promise, 'reason:', reason)
})

process.on('uncaughtException', (error) => {
  console.log('Uncaught Exception:', error)
})