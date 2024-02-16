from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
import os
import asyncio

app = FastAPI()


@app.post("/upload-msh/")
async def create_upload_file(file: UploadFile = File(...)):
    try:
        # Ensure there's a directory to save the uploaded files
        os.makedirs("uploaded_files", exist_ok=True)

        file_location = f"uploaded_files/{file.filename}"
        with open(file_location, "wb+") as file_object:
            file_object.write(file.file.read())

        # Placeholder for running PyFR simulation
        # You would pass the file_location and any other required parameters to your PyFR simulation function here
        simulation_result = await run_pyfr_simulation(file_location)

        return {"filename": file.filename, "result": simulation_result}
    except Exception as e:
        return JSONResponse(status_code=400, content={"message": f"An error occurred: {str(e)}"})


async def run_pyfr_simulation(mesh_file_path):
    # This function is where you would set up and run your PyFR simulation
    # Given the complexity of CFD simulations, this is just a placeholder function
    # Assume we perform a simulation and return a simple result
    await asyncio.sleep(5)  # Simulate a delay for the simulation
    return "Simulation result placeholder" #test 0ig

