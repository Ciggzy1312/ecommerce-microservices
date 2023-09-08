import { basePublisher } from './base';
import log from '../../utils/logger';

export async function orderExpiredPublisher (order: any) {
    try {
        const exchangeName = "OrderExpired";
        const data = {
            _id: order._id,
            createdBy: order.createdBy,
        }

        const { message, error } = await basePublisher(exchangeName, data);

        if (error) {
            log.info(error);
            return;
        }

        log.info(message);
        return;
    } catch (error: any) {
        log.error(error.message);
        return;
    }
}