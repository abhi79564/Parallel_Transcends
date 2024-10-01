const handleDuplicateKeyError = (err, res) => {
  const field = Object.keys(err.keyValue);
  const code = 409;
  const error = `${field} already exists.`;
  res.status(code).send({ success: false, message: error });
};

const handleCastError = (err, res) => {
  const field = Object.keys(err.keyValue);
  const code = 409;
  res.status(code).send({ success: false, message: "field" });
};
const handleValidationError = (err, res) => {
  let errors = Object.values(err.errors).map((el) => el.message);
  let fields = Object.values(err.errors).map((el) => el.path);
  let code = 400;

  if (
    (fields[0] == "eventDate" || fields[0] == "lastDate") &&
    errors[0].slice(0, 12) === "Cast to date"
  ) {
    res.status(code).send({ success: false, message: "Invalid date format" });
  } else {
    res.status(code).send({ success: false, message: errors[0] });
  }
};

//error controller function
module.exports = (err, req, res, next) => {
  try {
    console.log("congrats you hit the error middleware");
    if (err.errors.name === "CastError")
      return (err = handleCastError(err, res));
    if (err.name === "ValidationError")
      return (err = handleValidationError(err, res));
    if (err.code && err.code == 11000)
      return (err = handleDuplicateKeyError(err, res));
  } catch (err) {
    console.log(err);
    res.status(500).send("An unknown error occured.");
  }
};
