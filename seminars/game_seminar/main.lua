
-- [[ block comments like this]]


-- Set width and stuff, the constants will be used with the push:setupScreen function
VIRTUAL_WIDTH = 384
VIRTUAL_HEIGHT = 216
WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720

PADDLE_WIDTH = 8
PADDLE_HEIGHT = 32

-- to import the logic from push.lua
push = require "push"

player1 = {
    x = 10, y = 10
}

player2 = {
    x = VIRTUAL_WIDTH - PADDLE_WIDTH - 10, y = VIRTUAL_HEIGHT - PADDLE_HEIGHT - 10
}


function love.load()
    love.graphics.setDefaultFilter("nearest", "nearest")
    push:setupScreen(VIRTUAL_WIDTH, VIRTUAL_HEIGHT, WINDOW_WIDTH, WINDOW_HEIGHT)
end


function love.update(dt)

end

function love.keypressed(key)
    if key == "escape" then
        love.event.quit()
    end
end


function love.keypressed(key)

end


function love.draw()
    push:start()
    love.graphics.clear(40/255, 45/255, 52/255, 255/255)
    love.graphics.rectangle("fill", player1.x, player1.y, PADDLE_WIDTH, PADDLE_HEIGHT)
    love.graphics.rectangle("fill", player2.x, player2.y, PADDLE_WIDTH, PADDLE_HEIGHT)
    push:finish()
 end