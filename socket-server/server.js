import express from "express"; // not {} because it's not a named export
import { createServer } from "http";
import  cors  from "cors";
import { Server } from "socket.io";
import fetch from "node-fetch";

// dictionary to store <player color, socket id>
// Now assuming that 1st: red, 2nd: blue, 3rd: green, 4th: yellow (may change)
const player_color_to_socket_id = {
    "red": "",
    "blue": "",
    "green": "",
    "yellow": ""
}

const color = ["red", "blue", "green", "yellow"];
let count_person = 0;


const app = express();
const server = createServer(app);
const io = new Server(server, {
  cors: {
    origin: "*",
  }
});

app.use(cors());

io.on('connection', socket => {
    console.log('Client connected');

    // fixme - set at max 4 players, now is accepting the fith
    socket.on("join_room", () => {
        // map player color to socket id
        player_color_to_socket_id[color[count_person]] = socket.id;
        count_person += 1;
        io.emit("join_room", JSON.stringify(player_color_to_socket_id));
        console.log(player_color_to_socket_id)
    })

    socket.on("start_game", () => {
        // todo need to make the JSON for game_config
        // not from client, but generate from socket server
        const game_config = {
            "num_of_human_player": count_person, 
            "num_of_ai_player": 4 - count_person, 
            "color_of_player": ["red", "blue", "green", "yellow"], 
            "board_size": 3
        }


        fetch('http://localhost:8000/start_game', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(game_config)
        })
        .then(response => response.json())
        .then(data => {
            console.log(data);
            io.emit("start_game", data);
        });
    })


    // todo - need to change it to get request format
    socket.on("roll_dice", (req) => {
        const queryParams = new URLSearchParams(req).toString();
        fetch('http://localhost:8000/roll_dice?' + queryParams, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
            }
        })
        .then(response => response.json())
        .then(data => {
            console.log(data);
            io.emit("roll_dice", data);
        });
    })



    socket.on("end_turn", (player_info) => {
        const queryParams = new URLSearchParams(player_info).toString();
        fetch('http://localhost:8000/end_turn?' + queryParams, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
            }
        })
        .then(response => response.json())
        .then(data => {
            console.log(data);
            io.emit("end_turn", data);
        });
    })

    // todo - current player
    socket.on("current_player", (req) => {
        const queryParams = new URLSearchParams(req).toString();
        fetch('http://localhost:8000/current_player?' + queryParams, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
            }
        })
        .then(response => response.json())
        .then(data => {
            console.log(data);
            io.emit("current_player", data);
        });
    })

    socket.on("board_state", (player_info) => {
        const queryParams = new URLSearchParams(player_info).toString();
        fetch('http://localhost:8000/board_state?' + queryParams, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
            }
        })
        .then(response => response.json())
        .then(data => {
            console.log(data);
            io.emit("board_state", data);
        });
    })

    socket.on("updated_player_resource", (player_info) => {
        const queryParams = new URLSearchParams(player_info).toString();
        fetch('http://localhost:8000/updated_player_resource?' + queryParams, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
            }
        })
        .then(response => response.json())
        .then(data => {
            console.log(data);
            io.emit("updated_player_resource", data);
        });
    })

    socket.on("player_resources", (player_info) => {
        const queryParams = new URLSearchParams(player_info).toString();
        fetch('http://localhost:8000/player_resources?' + queryParams, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
            }
        })
        .then(response => response.json())
        .then(data => {
            console.log(data);
            io.emit("player_resources", data);
        });
    })

    socket.on("available_actions", (player_info) => {
        const queryParams = new URLSearchParams(player_info).toString();
        fetch('http://localhost:8000/available_actions?' + queryParams, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
            }
        })
        .then(response => response.json())
        .then(data => {
            console.log(data);
            socket.emit("available_actions", data);
        });
    })
    

    // {infrastucture} as roads, settlements, cities
    socket.on("valid_location/roads", (req) => {
        const queryParams = new URLSearchParams(req).toString();
        fetch('http://localhost:8000/valid_location/roads?' + queryParams, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
            }
        })
        .then(response => response.json())
        .then(data => {
            console.log(data);
            socket.emit("valid_location/roads", data);
        });
    })
    
    socket.on("valid_location/cities", (req) => {
        const queryParams = new URLSearchParams(req).toString();
        fetch('http://localhost:8000/valid_location/cities?' + queryParams, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
            }
        })
        .then(response => response.json())
        .then(data => {
            console.log(data);
            socket.emit("valid_location/cities", data);
        });
    })

    socket.on("valid_location/settlements", (req) => {
        const queryParams = new URLSearchParams(req).toString();
        fetch('http://localhost:8000/valid_location/settlements?' + queryParams, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
            }
        })
        .then(response => response.json())
        .then(data => {
            console.log(data);
            socket.emit("valid_location/settlements", data);
        });
    })

    // {infrastucture} as roads, settlements, cities for build 
    socket.on("build/roads", (req) => {
        // const queryParams = new URLSearchParams(req).toString();
        fetch('http://localhost:8000/build/roads', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(req)
        })
        .then(response => response.json())
        .then(data => {
            console.log(data);
            socket.emit("build/roads", data);
        });
    })
    
    socket.on("build/cities", (req) => {
        
        // const queryParams = new URLSearchParams(req).toString();
        console.log(req)
        fetch('http://localhost:8000/build/cities', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(req)
        })
        .then(response => response.json())
        .then(data => {
            console.log(data);
            socket.emit("build/cities", data);
        });
    })

    socket.on("build/settlements", (req) => {
        // const queryParams = new URLSearchParams(req).toString();
        fetch('http://localhost:8000/build/settlements', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(req)
        })
        .then(response => response.json())
        .then(data => {
            console.log(data);
            socket.emit("build/settlements", data);
        });
    })
    

    socket.on("valid_robber_locations", (player_info) => {
        const queryParams = new URLSearchParams(player_info).toString();
        fetch('http://localhost:8000/valid_robber_locations?' + queryParams, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
            }
        })
        .then(response => response.json())
        .then(data => {
            console.log(data);
            socket.emit("valid_robber_locations", data);
        });
    })

    socket.on("num_discard_resource_card", (player_info) => {
        const queryParams = new URLSearchParams(player_info).toString();
        fetch('http://localhost:8000/num_discard_resource_card?' + queryParams, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
            }
        })
        .then(response => response.json())
        .then(data => {
            console.log(data);
            socket.emit("num_discard_resource_card", data);
        });
    })

    socket.on("discard_resource_card", (resourceInfo) => {
        fetch('http://localhost:8000/discard_resource_card', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(resourceInfo)
        })
        .then(response => response.json())
        .then(data => {
            console.log(data);
            socket.emit("discard_resource_card", data);
        });
    })

    socket.on("place_robber", (tileInfo) => {
        fetch('http://localhost:8000/place_robber', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(tileInfo)
        })
        .then(response => response.json())
        .then(data => {
            console.log(data);
            socket.emit("place_robber", data);
        });
    })

    socket.on("buy_dev_card", (playerInfo) => {
        fetch('http://localhost:8000/buy_dev_card', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(playerInfo)
        })
        .then(response => response.json())
        .then(data => {
            console.log(data);
            socket.emit("buy_dev_card", data);
        });
    })

    socket.on("player_dev_cards", (player_info) => {
        const queryParams = new URLSearchParams(player_info).toString();
        fetch('http://localhost:8000/player_dev_cards?' + queryParams, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
            }
        })
        .then(response => response.json())
        .then(data => {
            console.log(data);
            io.emit("player_dev_cards",data);
        });
    })

    socket.on("visible_victory_points", (player_info) => {
        const queryParams = new URLSearchParams(player_info).toString();
        fetch('http://localhost:8000/visible_victory_points?' + queryParams, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
            }
        })
        .then(response => response.json())
        .then(data => {
            console.log(data);
            io.emit("visible_victory_points",data);
        });
    })

    socket.on("victory_points", (player_info) => {
        const queryParams = new URLSearchParams(player_info).toString();
        fetch('http://localhost:8000/victory_points?' + queryParams, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
            }
        })
        .then(response => response.json())
        .then(data => {
            console.log(data);
            io.emit("victory_points", data);
        });
    })


    
    socket.on("leaderboard", (req) => {
        const queryParams = new URLSearchParams(req).toString();
        fetch('http://localhost:8000/leaderboard?' + queryParams, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
            }
        })
        .then(response => response.json())
        .then(data => {
            console.log(data);
            io.emit("leaderboard", data);
        });
    })


    // trade
    socket.on("trade/start", (tradeInfo) => {
        fetch('http://localhost:8000/trade/start', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(tradeInfo)
        })
        .then(response => response.json())
        .then(data => {
            console.log(data);
            // need to parse data, and send to the specific player
            players = data.players;
            for (let index = 0; index < players.length; index++) {
                io.to(player_color_to_socket_id[players[index]]).emit("trade/start", data)
            };
        });
    })


    socket.on("trade/accept", (tradeInfo) => {
        fetch('http://localhost:8000/trade/accept', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            }
        })
    })
            


  socket.on('disconnect', () => {
    console.log('Client disconnected');
  });
});
    



const port = 3001;
server.listen(port, () => {
    console.log(`Server listening on port ${port}`);
});
