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

//   socket.on('getNumber', () => {
//     // const number = Math.floor(Math.random() * 100);
//     // send request to game-logic server
//     fetch('http://localhost:8000/')
//       .then(response => response.json())
//       .then(data => {
//         console.log(data);
//         io.emit('number', { number: data.number });
//       })
//     // console.log(`Generated number: ${number}`);
//     // io.emit('number', { number });
//     // socket emit sends to one client
//     // io emit sends to all clients
//   });


    // Demo of sending data from client to server
    // POST request demo
//   socket.on('getNumber', (numberTest) => {
//     console.log(numberTest);
//     fetch('http://localhost:8000/getNumber', {
//         method: 'POST',
//         headers: {
//             'Content-Type': 'application/json'
//         },
//         body: JSON.stringify(numberTest)
//         })
//         .then(response => response.json())
//         .then(data => {
//             console.log(data);
//             io.emit(data);
//         });
//     })

//    // GET request demo
    // socket.on('getNumber', (numberTest) => {
    //     console.log(numberTest);
    //     fetch('http://localhost:8000/getNumber', {
    //         method: 'GET',
    //         headers: {
    //             'Content-Type': 'application/json',
    //             'X-Game-Config': JSON.stringify(game_config)
    //         }
    //         })
    //         .then(response => response.json())
    //         .then(data => {
    //             console.log(data);
    //             io.emit(data);
    //         });
    //     })


    // fixme - set at max 4 players, now is accepting the fith
    socket.on("join_room", () => {
        // map player color to socket id
        player_color_to_socket_id[color[count_person]] = socket.id;
        count_person += 1;
        io.emit("join_room", JSON.stringify(player_color_to_socket_id));
        console.log(player_color_to_socket_id)
    })


    socket.on("add_player", (playerInfo) => {
        fetch('http://localhost:8000/add_player', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(playerInfo)
        })
        .then(response => response.json())
        .then(data => {
            console.log(data);
            io.emit("add_player", data);
        });
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

    socket.on("dump_games", () => {
        fetch('http://localhost:8000/dump_games', {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json'
            }
        });
    })

    // todo - need to change it to get request format
    socket.on("roll_dice", (game_config) => {
        fetch('http://localhost:8000/roll_dice', {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                'X-Game-Config': JSON.stringify(game_config)
            }
        })
        .then(response => response.json())
        .then(data => {
            console.log(data);
            io.emit("rool_dice", data);
        });
    })

    socket.on("end_turn", (player_info) => {
        fetch('http://localhost:8000/end_turn', {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                'X-Game-Config': JSON.stringify(player_info)
            }
        })
        .then(response => response.json())
        .then(data => {
            console.log(data);
            io.emit("end_turn", data);
        });
    })

    socket.on("board_state", (player_info) => {
        fetch('http://localhost:8000/board_state', {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                'X-Game-Config': JSON.stringify(player_info)
            }
        })
        .then(response => response.json())
        .then(data => {
            console.log(data);
            io.emit("board_state", data);
        });
    })

    socket.on("updated_player_resource", (player_info) => {
        fetch('http://localhost:8000/updated_player_resource', {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                'X-Game-Config': JSON.stringify(player_info)
            }
        })
        .then(response => response.json())
        .then(data => {
            console.log(data);
            io.emit("updated_player_resource", data);
        });
    })

    socket.on("player_resources", (player_info) => {
        fetch('http://localhost:8000/player_resources', {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                'X-Game-Config': JSON.stringify(player_info)
            }
        })
        .then(response => response.json())
        .then(data => {
            console.log(data);
            io.emit("player_resources", data);
        });
    })

    socket.on("available_actions", (player_info) => {
        fetch('http://localhost:8000/available_actions', {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                'X-Game-Config': JSON.stringify(player_info)
            }
        })
        .then(response => response.json())
        .then(data => {
            console.log(data);
            io.emit("available_actions", data);
        });
    })
    

    // {infrastucture} as roads, settlements, cities
    socket.on("valid_location/roads", (req) => {
        fetch('http://localhost:8000/valid_location/roads', {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                'X-Game-Config': JSON.stringify(req)
            }
        })
        .then(response => response.json())
        .then(data => {
            console.log(data);
            io.emit("valid_location/roads", data);
        });
    })
    
    socket.on("valid_location/cities", (req) => {
        fetch('http://localhost:8000/valid_location/cities', {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                'X-Game-Config': JSON.stringify(req)
            }
        })
        .then(response => response.json())
        .then(data => {
            console.log(data);
            io.emit("valid_location/cities", data);
        });
    })

    socket.on("valid_location/settlements", (req) => {
        fetch('http://localhost:8000/valid_location/settlements', {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                'X-Game-Config': JSON.stringify(req)
            }
        })
        .then(response => response.json())
        .then(data => {
            console.log(data);
            io.emit("valid_location/settlements", data);
        });
    })

    // {infrastucture} as roads, settlements, cities for build 
    socket.on("build/roads", (req) => {
        fetch('http://localhost:8000/build/roads', {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                'X-Game-Config': JSON.stringify(req)
            }
        })
        .then(response => response.json())
        .then(data => {
            console.log(data);
            io.emit("build/roads", data);
        });
    })
    
    socket.on("build/cities", (req) => {
        fetch('http://localhost:8000/build/cities', {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                'X-Game-Config': JSON.stringify(req)
            }
        })
        .then(response => response.json())
        .then(data => {
            console.log(data);
            io.emit("build/cities", data);
        });
    })

    socket.on("build/settlements", (req) => {
        fetch('http://localhost:8000/build/settlements', {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                'X-Game-Config': JSON.stringify(req)
            }
        })
        .then(response => response.json())
        .then(data => {
            console.log(data);
            io.emit("build/settlements", data);
        });
    })
    

    socket.on("valid_robber_locations", (player_info) => {
        fetch('http://localhost:8000/valid_robber_locations', {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                'X-Game-Config': JSON.stringify(player_info)
            }
        })
        .then(response => response.json())
        .then(data => {
            console.log(data);
            io.emit("valid_robber_locations", data);
        });
    })

    socket.on("num_discard_resource_card", (player_info) => {
        fetch('http://localhost:8000/discard_resource_card', {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                'X-Game-Config': JSON.stringify(player_info)
            }
        })
        .then(response => response.json())
        .then(data => {
            console.log(data);
            io.emit("num_discard_resource_card", data);
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
            io.emit("discard_resource_card", data);
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
            io.emit("place_robber", data);
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
            io.emit("buy_dev_card", data);
        });
    })

    socket.on("visible_victory_points", (player_info) => {
        fetch('http://localhost:8000/visible_victory_points', {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                'X-Game-Config': JSON.stringify(player_info)
            }
        })
        .then(response => response.json())
        .then(data => {
            console.log(data);
            io.emit("visible_victory_points",data);
        });
    })

    socket.on("visible_victory_points", (player_info) => {
        fetch('http://localhost:8000/visible_victory_points', {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                'X-Game-Config': JSON.stringify(player_info)
            }
        })
        .then(response => response.json())
        .then(data => {
            console.log(data);
            io.emit("visible_victory_points", data);
        });
    })

    socket.on("victory_points", (player_info) => {
        fetch('http://localhost:8000/victory_points', {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                'X-Game-Config': JSON.stringify(player_info)
            }
        })
        .then(response => response.json())
        .then(data => {
            console.log(data);
            io.emit("victory_points", data);
        });
    })
    
    // Leaderboard - todo


  socket.on('disconnect', () => {
    console.log('Client disconnected');
  });
});



const port = 3001;
server.listen(port, () => {
    console.log(`Server listening on port ${port}`);
});
