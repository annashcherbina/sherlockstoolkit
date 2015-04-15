name := "SnpMain"

version := "0.1"

scalaVersion := "2.10.3" 

libraryDependencies ++= Seq( "org.mongodb" %% "casbah" % "2.6.2", 
    "org.slf4j" % "slf4j-simple" % "1.6.4",
    "org.scala-lang" % "scala-actors" % "2.10.3"
 )

scalariformSettings
