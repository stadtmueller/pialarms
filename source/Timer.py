/*
This file is part of PiAlarms.

    PiAlarms is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    PiAlarms is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with PiAlarms.  If not, see <http://www.gnu.org/licenses/>.
*/


class Timer( threading.Thread ):
  def __init__( self, count, orgCount, signal ):
    threading.Thread.__init__( self )
    self.count = count
    self.orgCount = orgCount
    self.signal = signal

  def reset( self ):
    self.count = self.orgCount
    print( "Timer restored" )

  def run( self ):
    print( "Starting Timer:" )
    while not self.count == 0:
      if not stop.isSet():
        self.count -= 1
        time.sleep( 1.000 )
        print( "Timer @ " + str( self.count ) )
      else:
        break
    print( "Timer finished" )
    cleanAndExit()
    # Function to execute after timer was terminated
