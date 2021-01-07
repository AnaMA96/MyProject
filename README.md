# The playlists migrator! 🎶 

![](https://images.unsplash.com/photo-1483412033650-1015ddeb83d1?ixid=MXwxMjA3fDB8MHxzZWFyY2h8Nnx8bXVzaWN8ZW58MHx8MHw%3D&ixlib=rb-1.2.1&w=1000&q=80)

In this project I've created a program to migrate playlists from a music streaming service like Spotify to another like Deezer, both ways. 
## How did I do this?

I worked with [the Spotify API](https://developer.spotify.com/documentation/web-api/) and [the Deezer API](https://developers.deezer.com/api) to get the necessary information of the songs of each playlist, and then, created my own API with [Flask](https://flask.palletsprojects.com/en/1.1.x/) so I can make GET and POST requests.

## How can you use it?

As the API is deployed with [Docker](https://www.docker.com) and [Heroku](https://devcenter.heroku.com/categories/reference), the operation is as simple as entering [this link](https://playlistmigrator.herokuapp.com/) and select the migration flow: from Deezer to Spotify or from Spotify to Deezer? You will have to sign in (keep calm, the [OAuth2 protocol](https://oauth.net/2/) let the program make changes without taking your credentials but redirecting you back to the app once you've signed in), and... 'voilà'! it will start working.

## Improvements

- Migrate the complete profile like the followed artists, other followed profiles... not just the playlists.
- Include other music streaming services like Apple Music, Amazon Music... etc.
- If you have any suggestions... please, let me know!