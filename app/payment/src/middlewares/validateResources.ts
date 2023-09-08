import { Request, Response, NextFunction } from "express";
import { AnyZodObject } from "zod";


const validate = (schema: AnyZodObject) => (req: Request, res: Response, next: NextFunction) => {
    try {
        schema.parse(req.body);
        return next();
    } catch (error: any) {
        return res.status(400).json({ error: error.errors[0].message });
    }
}

export default validate;