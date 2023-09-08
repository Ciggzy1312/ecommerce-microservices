import express from 'express';
import cookieParser from 'cookie-parser';
import log from './utils/logger';
import connectDB from './utils/connect';
import dotenv from 'dotenv';
dotenv.config();

import router from './routes';
import { baseConsumer } from './events/subscribers/base';

const app = express();
app.use(express.json());
app.use(cookieParser());

app.use(router);

baseConsumer("OrderCreated", "Payment_OrderCreated");
baseConsumer("OrderCancelled", "Payment_OrderCancelled");

app.listen(8003, async () => {
    log.info('Payment service is running on port 8003');
    await connectDB();
});