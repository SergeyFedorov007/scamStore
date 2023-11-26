// http://deltoserver.ddns.net:8080/api/Schedule?firstDate=1701043200&secondDate=1701129599

import { URL_API } from "../../../config/apiRoute";
import { notification } from "antd";
import * as React from "react";

class ScheduleService {
  async getSchedule(firstData, secondData) {
    try {
      const requestUrl = `${URL_API}Schedule?firstDate=${firstData}&secondDate=${secondData}`;
      const response = await fetch(requestUrl);

      return response;
    } catch (err) {
      console.log(err)
      notification.error({ message: "Something wrong", description: "wrong" });
    }
  }
}

export default new ScheduleService();
