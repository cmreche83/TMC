# Pre-Requisite
Make sure you have Docker installed ( so Docker desktop or at least docker engine and docker compose if only in the CLI)

# How to Run
- To run this program, in the command prompt type : docker compose up
- Once this is done, open your web browser and in the address bar type: http://localhost:3000
- Once you finish, in order not to keep it running in the background for nothing : docker compose down

# Few extras
- you can check directly what fastapi shows:
    http://localhost:8000/users
- you can also use curl to exchange request with fastapi.
- Extra hardening/consideration should be taken for a prod environment
- Should you want to try to do things fresh again ... I added the reset.sh file ( you should not needed it ).
This will delete any non running container and their volumes system wise. Use it at your own risks.
