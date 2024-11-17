from . import db

class AirQualityData(db.Model):
    __tablename__ = 'PollutantHistory'  # Name of the table in your database

    id = db.Column(db.Integer, primary_key=True)  # Unique ID for each record
    date_local = db.Column(db.Date, nullable=False)  # Date of the reading
    pollutants = db.Column(db.String(50), nullable=False)  # Pollutant type (e.g., PM2.5)
    county = db.Column(db.String(100), nullable=False)  # County name
    arithmetic_mean = db.Column(db.Float, nullable=False)  # Arithmetic mean of pollutant concentration

    def __repr__(self):
        return f"<AirQualityData {self.pollutants} in {self.county} on {self.date_local}>"
