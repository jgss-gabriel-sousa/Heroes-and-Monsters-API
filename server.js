require("dotenv").config();

const express = require("express");
const fs = require("fs");
const path = require("path");

const app = express();
const port = process.env.PORT;

async function readJSONFile(filePath){
    try{
        const data = await fs.promises.readFile(filePath);
        return JSON.parse(data);
    }catch(err){
        throw new Error(`Error reading file: ${filePath}`);
    }
}

app.get(`/:dataType/:jsonFile`, async (req, res) => {
    const fileName = req.params.jsonFile + ".json";
    const dataType = req.params.dataType;
    const filePath = path.join(__dirname, "data/"+dataType, fileName);

    try {
        const data = await readJSONFile(filePath);
        res.status(200).json(data);
    } catch (err) {
        console.error(err);
        res.status(404).send(`File not found: ${filePath}`);
    }
});

app.use((err, req, res, next) => {
    console.error(err);
    return res.status(500).send("An internal error occurred");
});

app.listen(port, () => {
    console.log(`Server running on port ${port}`);
});