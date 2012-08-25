#!/usr/bin/python
# vim:ts=8:sw=4:expandtab:encoding=utf-8
#
# Copyright © 2000,2001,2002,2003,2004,2005,2006,2007,2008,
# King Cheung, Shu <mozbugbox@yahoo.com.au>
#
# Copyright (c) 2012, Dave Crossland <dave@understandingfonts.com>
# 
# Redistribution and use in source and binary forms, with or without 
# modification, are permitted provided that the following conditions 
# are met:
# 
# Redistributions of source code must retain the above copyright 
# notice, this list of conditions and the following disclaimer.
# 
# Redistributions in binary form must reproduce the above 
# copyright notice, this list of conditions and the following
# disclaimer in the documentation and/or other materials provided 
# with the distribution.
# 
# The name of the author may not be used to endorse or promote
# products derived from this software without specific prior
# written permission.
# 
# THIS SOFTWARE IS PROVIDED BY THE AUTHOR ``AS IS'' AND ANY 
# EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, 
# THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A 
# PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE AUTHOR 
# BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, 
# EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED 
# TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, 
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND 
# ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT 
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING 
# IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF 
# THE POSSIBILITY OF SUCH DAMAGE. 
# 
# From http://comments.gmane.org/gmane.comp.fonts.fontforge.user/2573
#
# This is a FontForge python script to retract control points to 0. 
# Simply copy it to ~/.Fontforge/python/ and you will
# have a "Tools/Points/" menu. 
'''Retract control points of a on curve point to 0.'''

# see http://fontforge.sourceforge.net/uitranslationnotes.html#HotKeys
RETRACT_PREV_CP_KEY="Alt+8"
RETRACT_NEXT_CP_KEY="Alt+9" # could be None
RETRACT_BOTH_CP_KEY="Alt+0"

import sys
import fontforge

def retractcontrol(data, glyph):
   '''Retract control point menu function.'''
   glyph.preserveLayerAsUndo()
   points = []
   if not glyph.activeLayer:
       return
   layer = glyph.layers[glyph.activeLayer]
   for i in range(len(layer)):
       for j in range(len(layer[i])):
           p = layer[i][j]
           if p.selected:
               points.append((i,j))
   for p in points:
       retract(p, data, glyph)

def retract(p, direct, glyph):
   '''Retract control point of a point.
   p: (contour_index, point_index)
   direction: -1, 0, 1 for previous, both, next control point.
   '''
   glyph.preserveLayerAsUndo()
   layer = glyph.layers[glyph.activeLayer]
   contour = layer[p[0]]
   if len(contour) < 2:
       return
   cindex = p[0]
   pindex = p[1]

   point = contour[pindex]
   cpoint = [] # control points
   if direct in [0, -1]: # previous control
       try:
           if not contour[pindex-1].on_curve:
               cpoint.append((cindex, pindex-1))
       except IndexError:
           pass

   if direct in [0, 1]:
       try:
           if not contour[pindex+1].on_curve:
               cpoint.append((cindex, pindex+1))
       except IndexError:
           pass

   for c in cpoint:
       layer[c[0]][c[1]].x = point.x
       layer[c[0]][c[1]].y = point.y
   glyph.layers[glyph.activeLayer] = layer

if fontforge.hasUserInterface():
   fontforge.registerMenuItem(retractcontrol, None, -1,
           "Glyph", RETRACT_PREV_CP_KEY, "Points", "Retract Prev CP");
   fontforge.registerMenuItem(retractcontrol, None, 1,
           "Glyph", RETRACT_NEXT_CP_KEY, "Points", "Retract Next CP");
   fontforge.registerMenuItem(retractcontrol, None, 0,
           "Glyph", RETRACT_BOTH_CP_KEY, "Points", "Retract Both CP");
