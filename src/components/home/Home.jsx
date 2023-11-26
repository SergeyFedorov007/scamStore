import { useEffect, useState } from "react";
import { Button, Col, Form, Row, Select, Switch } from "antd";
import { optionsForHomeSelect, preparedFormItems } from "./constants";
import { UsergroupAddOutlined } from "@ant-design/icons";
import scheduleService from "../services/schedule"

import "./style.css";

const Home = () => {
  const [schedules, setSchedules] = useState([])
  const [webDevelop, setWebDevelop] = useState("")
  const [dataScience, setDataScience] = useState("")

  const [form] = Form.useForm();

  useEffect(() => {
    form.setFieldsValue({
      switch1: false,
      switch2: false,
      switch3: false,
      switch4: false,
      select: "web",
    });
  }, []);


  const getFields = async () => {
    const values = await form.validateFields();
    return {
      ...values,
      select: webDevelop + dataScience
    };
  };


  const getFirstDateAndSecondDate = () => {
    let currentDate = Math.floor(new Date().getTime() / 1000)
    return {
      firstDate: currentDate,
      secondDate: currentDate + 5 * 24 * 60 * 60
    }
  }

  return (
    <div className="home">
      <h3 className="welcome">Добро пожаловать</h3>
      <Form className="form" form={form}>
        <h4>Выберите подгруппу по английскому языку </h4>
        <div className="switch-container">
          {preparedFormItems.map((item) => {
            return (
              <Row
                align={"middle"}
                justify={"space-between"}
                key={item.name}
                className="form-item-row"
              >
                <Col span={16}>
                  <h4>
                    <UsergroupAddOutlined />
                    {" " + item.label}
                  </h4>
                </Col>
                <Col>
                  <Form.Item name={item.name}>
                    <Switch defaultChecked={false} />
                  </Form.Item>
                </Col>
              </Row>
            );
          })}
        </div>

        <Form.Item
          className="last-form-item"
          name="select"
          label={<h3 className="select-direction">Выберете направление</h3>}
          labelAlign={"left"}
        >
          <Select
            defaultOpen={true}
            options={optionsForHomeSelect}
            defaultValue={"web"}
            className="select"
          />
        </Form.Item>

   {/*     <h3 className="select-direction">Выберете направление</h3>
        <div className="last-form-item">
          <Button onClick={() => {
            setDataScience('')
            setWebDevelop("Web-develop")}}>Web-разработка</Button>
          <Button onClick={() => {
            setWebDevelop('')
            setDataScience("DataScience")}}>Наука о данных</Button>
        </div>*/}
        <div>
          <Button
            className="button-continue"
            type={"primary"}
            onClick={async () => {
             const data =  await scheduleService.getSchedule(getFirstDateAndSecondDate().firstDate, getFirstDateAndSecondDate().secondDate)
              setSchedules(data)
              //getFields().then((data) => {
                //console.log(data);
              //});
            }}
          >
            Продолжить
          </Button>
        </div>
      </Form>
    </div>
  );
};

export default Home;
