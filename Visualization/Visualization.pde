HashMap hm;
PImage mapImage;
PImage currentImage;
PImage [] allImages;
PFont font;
Table locationTable;
Table movieTable;
int rowCount;
float closestDist;
String closestText;
float closestTextX;
float closestTextY;


void setup()
{
  size(820,670);
  mapImage = loadImage("map.png");
  locationTable = new Table("locations.tsv");
  movieTable = new Table("NoFilmsByAbbrv.tsv");
  rowCount = locationTable.getRowCount();
  font = loadFont("ScalaSans-Regular-14.vlw");
  textFont(font);
  // Known number of images
  allImages = new PImage[221];
  hm = new HashMap();
  int currentIndex = 0;
  int idx = 0;
  for (int i = 0; i < rowCount; i+=1)
  {
    String abbrev = movieTable.getRowName(i);
    int num_results = movieTable.getInt(i, 1);
    if (num_results > 5)
      num_results = 5;
    for (idx = 0; idx < num_results; idx++)
    {
      allImages[currentIndex+idx] = loadImage(abbrev+str(idx)+".png");
    }
    // Put index of state in HashMap
    hm.put(abbrev, currentIndex);
    currentIndex += idx;
  }

}

void draw()
{
  background(255);
  image(mapImage,0,0);
  fill(230);
  smooth();
  noStroke();
  rect(0, 400, 820, 270);
  smooth();
  fill(192,0,0);
  noStroke();

  closestDist = MAX_FLOAT;

  for (int row = 0; row < rowCount; row++)
  {
    float x = locationTable.getFloat(row, 1);
    float y = locationTable.getFloat(row, 2);
    String abbrev = movieTable.getRowName(row);
    drawData (x, y, abbrev, row);
  }

  if (closestDist != MAX_FLOAT)
  {
    fill (0);
    textAlign (CENTER);
    text (closestText, closestTextX, closestTextY);
  }
}

void drawData (float x, float y, String abbrev, int row)
{
    int movieNum = movieTable.getInt(row, 1);
    float radius = map(movieNum, 0, 160, 1.8, 18);
    ellipseMode(RADIUS);
    ellipse(x,y, radius, radius);

    float d = dist (x, y, mouseX, mouseY);
    if ( ((d < radius + 2)) && (d < closestDist) )
    {
      closestDist = d;
      closestText = movieNum + " (" + abbrev + ")";
      closestTextX = x;
      closestTextY = y-radius-4;
      drawImgs (movieNum, abbrev);
    }
}

void drawImgs (int movieNum_, String abbrev_)
{
  int startingX = 20;
  int startingY = 450;
  int index = ((Integer) hm.get(abbrev_));
  int stateRow = movieTable.getRowIndex(abbrev_);
  int num = movieTable.getInt(stateRow, 1);
  num = num > 5 ? 5 : num;
    if (num >= 1)
      image(allImages[index], 10, 430, 142, 210);
     if (num >= 2)
       image(allImages[index + 1], 182, 430, 142, 210);
     if (num >= 3)
       image(allImages[index + 2], 344, 430, 142, 210);
     if (num >= 4)
       image(allImages[index + 3], 506, 430, 142, 210);
     if (num == 5)
       image(allImages[index + 4], 668, 430, 142, 210);

}



