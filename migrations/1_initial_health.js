// 2_deploy_contracts.js
const Health = artifacts.require("Health");

module.exports = function(deployer) {
  deployer.deploy(Health);
};