const express = require('express');
const { Alchemy, Network } = require("alchemy-sdk");

const cors = require('cors');


//env
require('dotenv').config()
const { APIKEY } = process.env



const config = {
  apiKey: APIKEY,
  network: Network.ETH_MAINNET,
};
const alchemy = new Alchemy(config);

const app = express();


const corsOptions = {
  origin: ['http://127.0.0.1:3002', 'http://127.0.0.1:3003'],
  optionsSuccessStatus: 204,
};


app.use(cors(corsOptions));



app.get('/nfts/:address', async (req, res) => {
  const address = req.params.address;

  try {
    const nfts = await alchemy.nft.getNftsForOwner(address);
    res.json(nfts.ownedNfts.slice(0, 15)); // 最初の15個のNFTだけを返す
  } catch (error) {
    console.error(error);
    res.status(500).send('Internal Server Error');
  }
});


app.listen(3000, () => {
  console.log('Server is running on http://localhost:3000/');
});
