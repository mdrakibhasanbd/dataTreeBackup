
// Select the database to use.
use('mongodbVSCodePlaygroundDB');
db.sales.aggregate([
    {
      $lookup: {
        from: "users",
        localField: "parrent_id",
        foreignField: "parrent_id",
        as: "router"
      }
    },
    {
      $match: {
        router: { $ne: [] }
      }
    }
  ]);
  
  