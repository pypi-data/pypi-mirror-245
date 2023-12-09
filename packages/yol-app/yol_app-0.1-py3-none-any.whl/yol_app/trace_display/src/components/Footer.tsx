/*
Copyright 2023 NeuralBridge AI

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
 */
import React from "react";
import Typography from "@material-ui/core/Typography";
import "./Footer.css";

const Footer: React.FC = () => {
  return (
    <footer className="footer">
      <a
        href="https://www.neuralbridge.ai/"
        target="_blank"
        className="footer__company-name"
      >
        Neural Bridge
      </a>
      <div className="footer__links">
        <a href="https://www.neuralbridge.ai/" className="footer__link">
          About
        </a>
        <a href="https://www.neuralbridge.ai/" className="footer__link">
          Contact
        </a>
        <a href="https://www.neuralbridge.ai/" className="footer__link">
          Terms of Service
        </a>
        <a href="https://www.neuralbridge.ai/" className="footer__link">
          Privacy Policy
        </a>
      </div>
      <Typography variant="body2" color="textSecondary" align="center">
        © 2023 Neural Bridge. All rights reserved.
      </Typography>
    </footer>
  );
};

export default Footer;
