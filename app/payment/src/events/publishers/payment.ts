import { basePublisher } from './base';
import log from '../../utils/logger';

export async function paymentSuccessPublisher (data: any) {
    try {
        const exchangeName = "PaymentCompleted"
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