import { NextFunction, Request, Response } from "express";
import jwt from "jsonwebtoken";
import log from "../utils/logger";

const authMiddleware = (req: Request, res: Response, next: NextFunction) => {
    try {
        const token = req.cookies.token || req.headers.cookie;
        if (!token) {
            return res.status(401).json({ message: "Unauthorized" });
        }

        const decoded = jwt.verify(token, process.env.SECRET_KEY!);
        req.user = decoded;
        next();
    } catch (error) {
        log.error(error);
        return res.status(401).json({ message: "Error validating token" });
    }
};

export default authMiddleware;