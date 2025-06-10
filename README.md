# Elementary-Flows

## GOAL OF THE PROJECT 

Conceived as a simple potential flow visualizer, this project now aims to develop and validate a full _vortex/source-sink panel method_ software. Boundary layer effects on aerodynamic performance are currently excluded.

## HOW MATH WORKS

This project constructs complex flow fields from four elementary flows: _uniform flow_, _source/sink_, _vortex_ and _doublet_. For simplicity, their polar coordinates are converted to cartesian coordinates using the following transformation:

[WORK IN PROGRESS]

Stream function and velocity field are represented here in both cylindrical and cartesian coordinates. In code, I use cartesian ones. The specific formulas for each elementary flow are presented below:

#### Uniform Flow

[WORK IN PROGRESS]

#### Source/Sink

[WORK IN PROGRESS]

#### Vortex

[WORK IN PROGRESS]

#### Doublet

[WORK IN PROGRESS]

Finally, the coefficient of pressure _Cp_ is calculated based on the free stream velocity and the local velocity at each point using the following equation:

[WORK IN PROGRESS]
